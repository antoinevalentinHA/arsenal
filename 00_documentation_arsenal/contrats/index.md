# 📋 Index — Contrats fonctionnels Arsenal

> **Porte d'entrée navigation.** Ce document liste l'ensemble des contrats
> fonctionnels du système Arsenal.
> Pour le rôle, le statut et les principes des contrats :
> voir [README.md](./README.md).

---

## Contrats plats (racine)

### Présence et contexte humain

| Contrat | Objet |
|---|---|
| [presence.md](./presence.md) | Règles de présence humaine |
| [vacances.md](./vacances.md) | Domaine vacances |
| [visite.md](./visite.md) | Contexte visite |
| [babysitting.md](./babysitting.md) | Contexte babysitting |
| [reveils.md](./reveils.md) | Réveils nocturnes enfants — observabilité, reset, babyphone opt-in |
| [simulation_presence.md](./simulation_presence.md) | Simulation de présence |
| [mobile.high_accuracy.contextuel.md](./mobile.high_accuracy.contextuel.md) | Géolocalisation haute précision contextuelle |
| [bssid.md](./bssid.md) | Référentiel BSSID maison |

### Système et infrastructure

| Contrat | Objet |
|---|---|
| [arsenal_nas.md](./arsenal_nas.md) | Domaine `arsenal_nas` |
| [arsenal_self.md](./arsenal_self.md) | Domaine `arsenal_self` |
| [ressources_lovelace.md](./ressources_lovelace.md) | Approvisionnement ressources frontend Lovelace |
| [zones.md](./zones.md) | Zones géographiques |
| [parametres_invalides.md](./parametres_invalides.md) | Paramètres invalides |
| [ping_lan_synthese.md](./ping_lan_synthese.md) | Synthèse ping LAN |
| [switchbot_transactionnel.md](./switchbot_transactionnel.md) | Socle transactionnel SwitchBot |
| [homekit_diagnostic.md](./homekit_diagnostic.md) | Diagnostic station Netatmo HomeKit |
| [ups_arret_ha.md](./ups_arret_ha.md) | UPS — arrêt Home Assistant |
| [notifications.md](./notifications.md) | Notifications |

### Énergie et équipements

| Contrat | Objet |
|---|---|
| [batteries.md](./batteries.md) | Batteries |
| [bluetti.md](./bluetti.md) | Domaine `energie_chaudiere` (Bluetti) |
| [energie.md](./energie.md) | Sources autorisées — dashboard Énergie |
| [cumulus_petite_maison.md](./cumulus_petite_maison.md) | Cumulus petite maison |

### Environnement physique et sécurité

| Contrat | Objet |
|---|---|
| [aeration_recommandation.md](./aeration_recommandation.md) | Recommandation aération (transversal) |
| [bouclage.md](./bouclage.md) | Bouclage ECS ⚠️ (voir §Anomalies) |
| [vmc.md](./vmc.md) | VMC |
| [volets_pluie.md](./volets_pluie.md) | Volets — pluie |
| [mouvements.md](./mouvements.md) | Mouvements |
| [voiture.md](./voiture.md) | Voiture — Audi A3 e-tron |

---

## Domaines (sous-dossiers)

| Domaine | Fichiers | Navigation | Description |
|---|:--:|---|---|
| [aeration_blocage_chauffage/](./aeration_blocage_chauffage/) | 37 | README ✅ | Machine d'état aération→blocage chauffage (m0→m6) |
| [alarme/](./alarme/) | 15 | — | Pipeline alarme numéroté 00→99 |
| [boiler/](./boiler/) | 7 | README ✅ | Chaudière / boiler bridge |
| [chauffage/](./chauffage/) | 52 | README ✅ | Pipeline chauffage + capteurs + amendements |
| [climatisation/](./climatisation/) | 39 | README ✅ | Climatisation (12 root + 26 capteurs) |
| [deshumidificateur/](./deshumidificateur/) | 2 | — | Déshumidificateur cave |
| [eclairage/](./eclairage/) | 5 | — | Éclairage |
| [ecs/](./ecs/) | 28 | — | ECS — fondation (00-11) + contrats d'exécution |
| [imprimerie/](./imprimerie/) | 3 | — | Bruit machines industrielles (Imprimerie Baillet) |
| [meteo/](./meteo/) | 16 | — | Météo — axes, palmarès, validation, sous-domaines |
| [ouvertures/](./ouvertures/) | 3 | — | Ouvertures (portes / fenêtres) |
| [pannes/](./pannes/) | 9 | — | Pannes — internet + secteur |
| [publication/](./publication/) | 1 | — | Publication |
| [sante/](./sante/) | 2 | — | Santé — cardio nocturne + sommeil Withings |

---

## Anomalies signalées (non corrigées)

1. **`bouclage.md` (racine) et `ecs/04_bouclage_ecs_sous_systeme.md`** : **résolu
   par renvoi** (ARB-2) — `bouclage.md` est le contrat canonique ;
   `ecs/04_bouclage_ecs_sous_systeme.md` est un renvoi sans doctrine autonome.
   Source unique de vérité.

2. **`aeration_recommandation.md` (racine) et `aeration_blocage_chauffage/`
   (sous-dossier)** : deux objets distincts portant la racine nominale
   `aeration_`. Distinction actée dans `carte_domaines.md` §5.7.
