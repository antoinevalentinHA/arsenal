# 📋 Index — Contrats fonctionnels Arsenal

> 🇬🇧 **English overview: [index.en.md](./index.en.md)**

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
| [resilience_integrations.md](./resilience_integrations.md) | Résilience des intégrations — séparation fraîcheur / disponibilité / recovery |
| [ups_arret_ha.md](./ups_arret_ha.md) | UPS — arrêt Home Assistant |
| [notifications.md](./notifications.md) | Notifications |

### Énergie et équipements

| Contrat | Objet |
|---|---|
| [batteries.md](./batteries.md) | Batteries |
| [bluetti.md](./bluetti.md) | Domaine `energie_chaudiere` (Bluetti) |
| [energie.md](./energie.md) | Sources autorisées — dashboard Énergie |
| [cumulus_petite_maison.md](./cumulus_petite_maison.md) | Cumulus petite maison |
| [electromenager.md](./electromenager.md) | Détection de cycle + notification (lave-vaisselle, buanderie) |

### Environnement physique et sécurité

| Contrat | Objet |
|---|---|
| [aeration_recommandation.md](./aeration_recommandation.md) | Recommandation aération (transversal) |
| [poele.md](./poele.md) | Poêle — apport thermique exogène : mémoire / blocage chauffage + climatisation (transversal) |
| [bouclage.md](./bouclage.md) | Bouclage ECS ⚠️ (voir §Anomalies) |
| [vmc.md](./vmc.md) | VMC |
| [volets_pluie.md](./volets_pluie.md) | Volets — pluie |
| [mouvements.md](./mouvements.md) | Mouvements |
| [voiture.md](./voiture.md) | Voiture — Audi A3 e-tron |

> **Note terminologique.** Le qualificatif « (transversal) » employé dans cet
> index signifie « à impact inter-domaines » ; il ne désigne **pas** le domaine
> d'ID `transversal` défini par
> [`prefixe_domaine_automatisations.md`](../architecture/03_doctrines/prefixe_domaine_automatisations.md)
> (domaine de préfixe **non créé** à ce jour). Ces contrats ont chacun un
> domaine propriétaire unique.

---

## Domaines (sous-dossiers)

| Domaine | Fichiers | Navigation | Description |
|---|:--:|---|---|
| [aeration_blocage_chauffage/](./aeration_blocage_chauffage/) | 37 | README ✅ | Machine d'état aération→blocage chauffage (m0→m6) |
| [alarme/](./alarme/) | 16 | README ✅ | Pipeline alarme numéroté 00→99 |
| [arrosage/](./arrosage/) | 19 | README ✅ | Arrosage jardin — coexistence gouvernée Arsenal ↔ Rain Bird (v0.1 ; observation v0 livrée ; **décision V1 paramétrable spécifiée**) + relevé pont MQTT, classification entités, pré-requis runtime, mode manuel supervisé, relevé capteurs humidité sol Zigbee, socle observation hydrique v0 (chapeau + qualité données sol + canal réservoir sol **livré** + canal demande climatique **spécifié**) + **contrat de décision d'arrosage V1** (mono-station, exécution déléguée au script Run supervisé) |
| [boiler/](./boiler/) | 7 | README ✅ | Chaudière / boiler bridge |
| [chauffage/](./chauffage/) | 52 | README ✅ | Pipeline chauffage + capteurs + amendements |
| [climatisation/](./climatisation/) | 43 | README ✅ | Climatisation (16 root + 27 capteurs) |
| [deshumidificateur/](./deshumidificateur/) | 3 | README ✅ | Déshumidificateur cave |
| [eclairage/](./eclairage/) | 7 | README ✅ | Éclairage |
| [ecs/](./ecs/) | 31 | README ✅ | ECS — fondation (00-11) + contrats d'exécution |
| [imprimerie/](./imprimerie/) | 4 | README ✅ | Bruit machines industrielles (Imprimerie) |
| [meteo/](./meteo/) | 23 | README ✅ | Météo — axes, palmarès, production pluie, validation, sous-domaines |
| [ouvertures/](./ouvertures/) | 4 | README ✅ | Ouvertures (portes / fenêtres) |
| [pannes/](./pannes/) | 11 | README ✅ | Pannes — internet + secteur |
| [publication/](./publication/) | 2 | README ✅ | Publication |
| [sante/](./sante/) | 3 | README ✅ | Santé — cardio nocturne + sommeil Withings |

---

## Anomalies signalées (non corrigées)

1. **`bouclage.md` (racine) et `ecs/04_bouclage_ecs_sous_systeme.md`** : **résolu
   par renvoi** (ARB-2) — `bouclage.md` est le contrat canonique ;
   `ecs/04_bouclage_ecs_sous_systeme.md` est un renvoi sans doctrine autonome.
   Source unique de vérité.

2. **`aeration_recommandation.md` (racine) et `aeration_blocage_chauffage/`
   (sous-dossier)** : deux objets distincts portant la racine nominale
   `aeration_`. Distinction actée dans `carte_domaines.md` §5.7.
