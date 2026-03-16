# CONTRAT ARSENAL — CLIMATISATION
## Index du dossier

**Domaine :** Climatisation résidentielle  
**Version contrat :** v1.2  
**Statut :** Stable — aligné implémentation Arsenal  

---

## Structure du dossier

| Fichier | Contenu |
|---|---|
| `01_finalite.md` | Finalité du système, états exclusifs, objectifs |
| `02_architecture.md` | Couches Arsenal, invariants globaux de déclenchement |
| `03_decision_canonique.md` | Objet `sensor.clim_target_mode`, pureté, déterminisme, séparation besoin/autorisation |
| `04_entrees_metier.md` | Températures, humidex, présence, contraintes physiques |
| `05_decision_candidats.md` | Règles de production des candidats par mode (COOL / DRY / HEAT / OFF) |
| `06_arbitrage_politique.md` | Politique d'arbitrage active, hiérarchie canonique des modes |
| `07_execution.md` | Application idempotente du mode cible |
| `08_securite.md` | Guards et Watchdog |
| `09_observabilite.md` | États explicatifs, robustesse, déterminisme post-redémarrage |
| `10_perimetre_exclu.md` | Ce que le système ne fait pas |

---

## Chaîne logique

```
Finalité
  └─ Architecture (couches)
       └─ Décision canonique (sensor.clim_target_mode)
            ├─ Entrées métier
            └─ Production des candidats
                 └─ Arbitrage (politique active)
                      └─ Exécution (idempotente)
                           └─ Sécurité (Guards / Watchdog — voie orthogonale)
                                └─ Observabilité (lecture seule)
```

---

⚠️ Principe Arsenal fondamental
La couche Exécution ne modifie jamais la décision.
Elle applique uniquement sensor.clim_target_mode.